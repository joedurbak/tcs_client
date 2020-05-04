
#include "SimpleAsyncConsumer.h"

//int main(int argc AMQCPP_UNUSED, char* argv[] AMQCPP_UNUSED) 
int main(int argc, char* argv[]) 
{
 
    activemq::library::ActiveMQCPP::initializeLibrary();
 
    // Set the URI to point to the IPAddress of your broker.
    // add any optional params to the url to enable things like
    // tightMarshalling or tcp logging etc.  See the CMS web site for
    // a full list of configuration options.
    //
    //  http://activemq.apache.org/cms/
    //
    std::string brokerURI =
        "failover://(tcp://jumar.lowell.edu:61616)";
 
    //============================================================
    // This is the Destination Name and URI options.  Use this to
    // customize where the consumer listens, to have the consumer
    // use a topic or queue set the 'useTopics' flag.
    //============================================================
    int mode = 0; 

    std::string destURI = "";
    if( argc > 1 ) destURI = argv[1]; 

    std::cout << "=====================================================\n";
    std::cout << "Starting   : Consumer" << std::endl;
    std::cout << "URI        : " << brokerURI << std::endl;
    std::cout << "Destination: " << destURI   << std::endl;
    std::cout << "-----------------------------------------------------\n";
 
    //============================================================
    // set to true to use topics instead of queues
    // Note in the code above that this causes createTopic or
    // createQueue to be used in the consumer.
    //============================================================
    //bool useTopics = false;
    bool useTopics = true;
 
    //============================================================
    // set to true if you want the consumer to use client ack mode
    // instead of the default auto ack mode.
    //============================================================
    bool clientAck = false;
    //bool clientAck = true;
 
    // Create the consumer
    SimpleAsyncConsumer consumer( brokerURI, destURI, useTopics, clientAck );
 
    // Start it up and it will listen forever.
    consumer.runConsumer();
 
    // Wait to exit.
    std::cout << "Press 'q' to quit" << std::endl;
    while( std::cin.get() != 'q') {}
 
    // All CMS resources should be closed before the library is shutdown.
    consumer.close();
 
    std::cout << "-----------------------------------------------------\n";
    std::cout << "Finished with the example." << std::endl;
    std::cout << "=====================================================\n";
 
    activemq::library::ActiveMQCPP::shutdownLibrary();
}

 
