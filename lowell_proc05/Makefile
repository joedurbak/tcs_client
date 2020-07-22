
BASEDIR = $(PWD)
INC_DIR = $(BASEDIR)/inc
SRC_DIR = $(BASEDIR)/src
OBJ_DIR = $(BASEDIR)/obj
BIN_DIR = $(BASEDIR)/bin

PROD = producer
CONS = consumer
CLSS = SimpleProducer SimpleAsyncConsumer 
PROG = $(PROD) $(CONS)

#activemq-cpp library
MQCPP_INC = -I/usr/local/include/activemq-cpp-3.10.0
MQCPP_LIB = -L/usr/local/lib -lactivemq-cpp

GNU_LIB   =  /usr/lib/x86_64-linux-gnu
APR_INC   =  -I/usr/include/apr-1.0
APR_LIB   =  -L$(GNU_LIB) -Wl,-rpath=$(GNU_LIB) -lapr-1

CXXDBG = -ggdb
CXXOPT = -Wall -O1 -fPIC $(CXXDBG)
CXXFLAGS = -I$(INC_DIR) $(CXXOPT) $(MQCPP_INC) $(APR_INC) -D_Darwin_
LDFLAGS  = -lncurses -lpthread -lreadline -ltermcap -lpanel $(MQCPP_LIB) $(APR_LIB)

INCS  = $(addprefix $(INC_DIR)/, $(addsuffix .h,  $(CLSS)))
OBJS  = $(addprefix $(OBJ_DIR)/, $(addsuffix .o,  $(CLSS)))
BINS  = $(addprefix $(BIN_DIR)/, $(PROG))

ALL: $(BINS)

$(OBJ_DIR)/%.o: $(SRC_DIR)/%.cc
	g++ $(CXXFLAGS) -c $< -o $@

$(BIN_DIR)/$(PROD): $(OBJ_DIR)/$(PROD).o $(OBJS) 
	g++ $(BINFLAGS) $(LDFLAGS) $^ -o $@

$(BIN_DIR)/$(CONS): $(OBJ_DIR)/$(CONS).o $(OBJS) 
	g++ $(BINFLAGS) $(LDFLAGS) $^ -o $@

clean:
	rm -f $(BIN_DIR)/* $(OBJ_DIR)/*

