all:
	javac *.java

run-server: Server.class Hello.class
	java -classpath . -Djava.rmi.server.codebase=file:./ Server 7000

run-client: Client.class Hello.class
	java  -classpath . Client localhost 7000

clean:
	$(RM) *~ *.class
