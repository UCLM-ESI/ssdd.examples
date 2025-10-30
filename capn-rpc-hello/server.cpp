#include <capnp/ez-rpc.h>
#include "hello.capnp.h"
#include <iostream>

class HelloI final: public Hello::Server {
public:
    kj::Promise<void> sendMsg(SendMsgContext context) override {
        auto message = context.getParams().getMessage();
        std::cout << "Server:no : " << message.cStr() << std::endl;
        return kj::READY_NOW;
    }
};

int main() {
    capnp::EzRpcServer server(kj::heap<HelloI>(), "localhost:4000");

    auto& waitScope = server.getWaitScope();
    kj::NEVER_DONE.wait(waitScope);
}
