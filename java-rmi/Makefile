all:
	javac *.java

run-server: Server.class Hello.class
	java -classpath . Server 

run-client: Client.class Hello.class
	java  -classpath . Client localhost

clean:
	$(RM) *~ *.class
