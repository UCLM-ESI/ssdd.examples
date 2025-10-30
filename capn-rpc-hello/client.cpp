#include <capnp/ez-rpc.h>
#include "hello.capnp.h"
#include <iostream>

int main(int argc, char* argv[]) {
    std::string address = (argc > 1) ? argv[1] : "127.0.0.1:4000";

    std::cout << "- Connecting to " << address << std::endl;

    capnp::EzRpcClient client(address);
    TextProcessor::Client textProcessor = client.getMain<TextProcessor>();

    auto request = textProcessor.upperRequest();
    request.setMessage("Hello world");

    auto& waitScope = client.getWaitScope();
    auto response = request.send().wait(waitScope);

    // Obtener y mostrar el resultado
    auto result = response.getResult();
    std::cout << "Server replies: " << result.cStr() << std::endl;
}
