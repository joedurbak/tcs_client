
#include "SimpleAsyncConsumer.h"

SimpleAsyncConsumer::~SimpleAsyncConsumer() 
{
  this->cleanup();
}
 
void SimpleAsyncConsumer::close() 
{
  this->cleanup();
}
 
void SimpleAsyncConsumer::runConsumer() 
{ 
  try {
    // Create a ConnectionFactory
    ActiveMQConnectionFactory* connectionFactory =
      new ActiveMQConnectionFactory( brokerURI );
 
    // Create a Connection
    connection = connectionFactory->createConnection();
    delete connectionFactory;
 
    ActiveMQConnection* amqConnection = dynamic_cast<ActiveMQConnection*>( connection );
    if( amqConnection != NULL ) {
      amqConnection->addTransportListener( this );
    }
 
    connection->start();
    connection->setExceptionListener(this);
 
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
 
    // Create a MessageConsumer from the Session to the Topic or Queue
    consumer = session->createConsumer( destination );
    consumer->setMessageListener( this );
  } catch (CMSException& e) {
    e.printStackTrace();
  }
}
 
void SimpleAsyncConsumer::onMessage( const Message* message )  
{
  static int count = 0;
 
  try {
    count++;
    const TextMessage* textMessage =
      dynamic_cast< const TextMessage* >( message );
    string text = "";
 
    if( textMessage != NULL ) {
      text = textMessage->getText();
    } else {
      text = "NOT A TEXTMESSAGE!";
    }
 
    if( clientAck ) {
      message->acknowledge();
    }
 
    printf( "Message #%d Received: %s\n", count, text.c_str() );
  } catch (CMSException& e) {
    e.printStackTrace();
  }
}
 
void SimpleAsyncConsumer::onException( const CMSException& ex AMQCPP_UNUSED ) 
{
  printf("CMS Exception occurred.  Shutting down client.\n");
  exit(1);
}
 
void SimpleAsyncConsumer::transportInterrupted() 
{
  std::cout << "The Connection's Transport has been Interrupted." << std::endl;
}
 
void SimpleAsyncConsumer::transportResumed() 
{
  std::cout << "The Connection's Transport has been Restored." << std::endl;
}
 
void SimpleAsyncConsumer::cleanup()
{
  try {
    if( connection != NULL ) {
      connection->close();
    }
  } catch ( CMSException& e ) { 
    e.printStackTrace(); 
  }

  if(destination) delete destination;
  if(consumer)    delete consumer;
  if(session)     delete session;
  if(connection)  delete connection;
  destination = NULL;
  consumer    = NULL;
  session     = NULL;
  connection  = NULL;
}
 
