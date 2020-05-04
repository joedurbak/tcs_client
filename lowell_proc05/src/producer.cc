
#include "SimpleProducer.h"

int main(int argc AMQCPP_UNUSED, char* argv[] AMQCPP_UNUSED) 
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
    // Total number of messages for this producer to send.
    //============================================================
    unsigned int numMessages = 1;
 
    //============================================================
    // This is the Destination Name and URI options.  Use this to
    // customize where the Producer produces, to have the producer
    // use a topic or queue set the 'useTopics' flag.
    //============================================================
    std::string destURI = "TCS.TCSSharedVariables.TCSSubData.TCSTcsCommandSV";


    std::cout << "=====================================================\n";
    std::cout << "Starting   : Producer" << std::endl;
    std::cout << "URI        : " << brokerURI << std::endl;
    std::cout << "Destination: " << destURI   << std::endl;
    std::cout << "-----------------------------------------------------\n";

 
    //============================================================
    // set to true to use topics instead of queues
    // Note in the code above that this causes createTopic or
    // createQueue to be used in the producer.
    //============================================================
    //bool useTopics = false;
    bool useTopics = true;
 
    // Create the producer and run it.
    SimpleProducer producer( brokerURI, numMessages, destURI, useTopics );
 
    // Publish the given number of Messages
    producer.run();
 
    // Before exiting we ensure that all CMS resources are closed.
    producer.close();
 
    std::cout << "-----------------------------------------------------\n";
    std::cout << "Finished with the example." << std::endl;
    std::cout << "=====================================================\n";
 
    activemq::library::ActiveMQCPP::shutdownLibrary();
}

