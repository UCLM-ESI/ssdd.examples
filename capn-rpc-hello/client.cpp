#include <capnp/ez-rpc.h>
#include "hello.capnp.h"
#include <iostream>

int main() {
    capnp::EzRpcClient client("localhost:4000");
    TextProcessor::Client textProcessor = client.getMain<TextProcessor>();

    auto request = textProcessor.upperRequest();
    request.setMessage("Hello world");

    auto& waitScope = client.getWaitScope();
    auto response = request.send().wait(waitScope);

    // Obtener y mostrar el resultado
    auto result = response.getResult();
    std::cout << "Server replies: " << result.cStr() << std::endl;
}
