#include <iostream>
#include <algorithm>
#include <string>
#include <ranges>
#include <capnp/ez-rpc.h>
#include "hello.capnp.h"

class TextProcessorI final: public TextProcessor::Server {
public:
    kj::Promise<void> upper(UpperContext context) override {
        auto message = context.getParams().getMessage();
        std::cout << "Client sent: " << message.cStr() << std::endl;

        std::string result = message;
        std::transform(
            message.begin(), message.end(),
            result.begin(), ::toupper);


        context.getResults().setResult(result);
        return kj::READY_NOW;
    }
};

int main() {
    capnp::EzRpcServer server(
        kj::heap<TextProcessorI>(), "localhost:4000");
    auto& waitScope = server.getWaitScope();
    kj::NEVER_DONE.wait(waitScope);
}
