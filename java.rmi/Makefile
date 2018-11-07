all:
	javac *.java

run-server: Server.class Hello.class
	java -classpath . -Djava.rmi.server.codebase=file:./ Server 9000

run-client: Client.class Hello.class
	java  -classpath . Client localhost 9000

clean:
	$(RM) *~ *.class
