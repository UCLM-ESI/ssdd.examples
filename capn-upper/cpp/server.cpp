#include <iostream>
#include <algorithm>
#include <string>
#include <ranges>
#include <capnp/ez-rpc.h>
#include "upper.capnp.h"

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

int main(int argc, char* argv[]) {
    std::string port = (argc > 1) ? argv[1] : "4000";
    std::string address = "0.0.0.0:" + port;

    std::cout << "- Server listening on " << address << std::endl;

    capnp::EzRpcServer server(
        kj::heap<TextProcessorI>(), address);
    auto& waitScope = server.getWaitScope();
    kj::NEVER_DONE.wait(waitScope);
}
