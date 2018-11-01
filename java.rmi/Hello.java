// From "Getting Started Using Java RMI"
// https://docs.oracle.com/javase/7/docs/technotes/guides/rmi/hello/hello-world.html

import java.rmi.Remote;
import java.rmi.RemoteException;

public interface Hello extends Remote {
    String sayHello() throws RemoteException;
}
