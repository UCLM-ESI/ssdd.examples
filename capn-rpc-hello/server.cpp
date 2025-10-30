#include <capnp/ez-rpc.h>
#include "hello.capnp.h"
#include <iostream>
#include <algorithm>
#include <string>

class HelloI final: public Hello::Server {
public:
    kj::Promise<void> sendMsg(SendMsgContext context) override {
        auto message = context.getParams().getMessage();
        std::cout << "Client sent: " << message.cStr() << std::endl;

        std::string result = message.cStr();
        std::transform(result.begin(), result.end(), result.begin(), ::toupper);

        context.getResults().setResult(result);
        return kj::READY_NOW;
    }
};

int main() {
    capnp::EzRpcServer server(kj::heap<HelloI>(), "localhost:4000");
    auto& waitScope = server.getWaitScope();
    kj::NEVER_DONE.wait(waitScope);
}
