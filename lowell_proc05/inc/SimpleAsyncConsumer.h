#ifndef _SIMPLE_ASYNC_CONSUMER_H
#define _SIMPLE_ASYNC_CONSUMER_H

#include <decaf/lang/Thread.h>
#include <decaf/lang/Runnable.h>
#include <decaf/util/concurrent/CountDownLatch.h>
#include <activemq/core/ActiveMQConnectionFactory.h>
#include <activemq/core/ActiveMQConnection.h>
#include <activemq/transport/DefaultTransportListener.h>
#include <activemq/library/ActiveMQCPP.h>
#include <decaf/lang/Integer.h>
#include <activemq/util/Config.h>
#include <decaf/util/Date.h>
#include <cms/Connection.h>
#include <cms/Session.h>
#include <cms/TextMessage.h>
#include <cms/BytesMessage.h>
#include <cms/MapMessage.h>
#include <cms/ExceptionListener.h>
#include <cms/MessageListener.h>
#include <stdlib.h>
#include <stdio.h>
#include <iostream>
 
using namespace activemq;
using namespace activemq::core;
using namespace activemq::transport;
using namespace decaf::lang;
using namespace decaf::util;
using namespace decaf::util::concurrent;
using namespace cms;
using namespace std;
 
class SimpleAsyncConsumer : public ExceptionListener,
                            public MessageListener,
                            public DefaultTransportListener {
private:
    Connection* connection;
    Session* session;
    Destination* destination;
    MessageConsumer* consumer;
    bool useTopic;
    std::string brokerURI;
    std::string destURI;
    bool clientAck;
 
private:
    SimpleAsyncConsumer( const SimpleAsyncConsumer& );
    SimpleAsyncConsumer& operator= ( const SimpleAsyncConsumer& );
 
public:
    SimpleAsyncConsumer( const std::string& brokerURI, const std::string& destURI,
                         bool useTopic = false, bool clientAck = false ) :
      connection(NULL), session(NULL), destination(NULL), consumer(NULL),
      useTopic(useTopic), brokerURI(brokerURI), destURI(destURI), 
      clientAck(clientAck) {}
 
    virtual ~SimpleAsyncConsumer();
    void close();
    void runConsumer(); 
 
    // Called from the consumer since this class is a registered MessageListener.
    virtual void onMessage( const Message* message );
 
    // If something bad happens you see it here as this class is also been
    // registered as an ExceptionListener with the connection.
    virtual void onException( const CMSException& ex AMQCPP_UNUSED );
    virtual void transportInterrupted();
    virtual void transportResumed();
 
private:
    void cleanup();
};

#endif
 
