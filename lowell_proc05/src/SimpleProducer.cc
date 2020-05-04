
#include "SimpleProducer.h"
#include <fstream>

SimpleProducer::~SimpleProducer()
{
  cleanup();
}
 
void SimpleProducer::close() 
{
  this->cleanup();
}
 
void SimpleProducer::run() 
{
  try {
    // Create a ConnectionFactory
    auto_ptr<ActiveMQConnectionFactory> connectionFactory(
      new ActiveMQConnectionFactory( brokerURI ) );
 
    // Create a Connection
    try{
      connection = connectionFactory->createConnection();
      connection->start();
    } catch( CMSException& e ) {
      e.printStackTrace();
      throw e;
    }
 
    // Create a Session
    if( clientAck ) {
      session = connection->createSession( Session::CLIENT_ACKNOWLEDGE );
    } else {
      session = connection->createSession( Session::AUTO_ACKNOWLEDGE );
    }
 
    // Create the destination (Topic or Queue)
    if( useTopic ) {
      destination = session->createTopic( destURI );
    } else {
      destination = session->createQueue( destURI );
    }
 
    // Create a MessageProducer from the Session to the Topic or Queue
    producer = session->createProducer( destination );
    producer->setDeliveryMode( DeliveryMode::NON_PERSISTENT );
 
    // Create the Thread Id String
    string threadIdStr = Long::toString( Thread::currentThread()->getId() );
 
    // Create a messages
    ifstream fin( "message.dat" );
    if( !fin ) return;  

    int    lid = 0;
    string text;
    string line;
    while( getline(fin,line) ) {
      if( lid++ > 0 ) text += "\n";
      text += line;
    }

    for( unsigned int ix=0; ix <numMessages; ++ix ){
      TextMessage* message = session->createTextMessage( text );
      message->setIntProperty( "Integer", ix );
 
      // Tell the producer to send the message
      printf( "Sent message #%d from thread %s\n", ix+1, threadIdStr.c_str() );
      producer->send( message );
      delete message;
    }
  }catch ( CMSException& e ) {
    e.printStackTrace();
  }
}
 
void SimpleProducer::cleanup()
{
  try {
    if( connection != NULL ) {
      connection->close();
    }
  } catch ( CMSException& e ) { 
    e.printStackTrace(); 
  }
        
  if(destination) delete destination;
  if(producer)    delete producer;
  if(session)     delete session;
  if(connection)  delete connection;
  destination = NULL;
  producer    = NULL;
  session     = NULL;
  connection  = NULL;
}
 
