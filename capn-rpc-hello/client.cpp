#include <capnp/ez-rpc.h>
#include "hello.capnp.h"
#include <iostream>

int main() {
    capnp::EzRpcClient client("localhost:4000");
    Hello::Client hello = client.getMain<Hello>();

    auto request = hello.sendMsgRequest();
    request.setMessage("Hello world");

    auto& waitScope = client.getWaitScope();
    request.send().wait(waitScope);

    std::cout << "Client: RPC completed" << std::endl;
}
