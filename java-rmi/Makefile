all:
	javac *.java

run-server: Server.class Hello.class
	java -classpath . -Djava.rmi.server.codebase=file:./ Server 

run-client: Client.class Hello.class
	java  -classpath . Client localhost

clean:
	$(RM) *~ *.class
