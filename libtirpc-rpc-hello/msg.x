/* msg.x: Remote msg printing protocol */

program MESSAGE_PROG {
  version PRINTMESSAGE_VERS {
    int PRINTMESSAGE(string) = 1;
  } = 1;
} = 600000000;
