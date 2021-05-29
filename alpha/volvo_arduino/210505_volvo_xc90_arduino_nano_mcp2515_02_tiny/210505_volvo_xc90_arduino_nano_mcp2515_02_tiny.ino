
#include <mcp2515.h>   

struct can_frame canMsg;
MCP2515 mcp2515(10);

void setup() 
{
  Serial.begin(9600);
  while (!Serial); 
  
  mcp2515.reset();
  mcp2515.setBitrate(CAN_125KBPS, MCP_8MHZ);
  mcp2515.setListenOnlyMode();  
}

void loop() 
{
  uint8_t irq = mcp2515.getInterrupts();
/*
  if(irq & MCP2515::CANINTF_ERRIF){
    uint8_t error = mcp2515.getErrorFlags();
    mcp2515.clearRXnOVRFlags();
    mcp2515.clearERRIF();
    //Serial.print("ERRIF.");
    //Serial.println();
    if(error & MCP2515::EFLG_RX0OVR){
      //Serial.print("EFLG_RX0OVR.");
      //Serial.println();
      mcp2515.clearRXnOVR();
      //mcp2515.reset();
      //mcp2515.setBitrate(CAN_125KBPS, MCP_8MHZ);
      //mcp2515.setListenOnlyMode();
    }
  }
  
  if(irq & MCP2515::CANINTF_MERRF){
    mcp2515.clearMERR();
    //Serial.print("MERRF.");
    //Serial.println();
  }
*/if (irq & MCP2515::CANINTF_RX0IF){
    mcp2515.readMessage(MCP2515::RXB0, &canMsg);
    Serial.print(canMsg.can_id, HEX); 
    Serial.print(" ");
    Serial.print(canMsg.can_id & CAN_EFF_MASK, HEX); 
    Serial.print(" "); 
    Serial.print(canMsg.can_dlc, HEX); 
    Serial.print(" ");   
    for (int i = 0; i<canMsg.can_dlc; i++){  
      Serial.print(canMsg.data[i],HEX);
      Serial.print(" ");
    }
    Serial.println();   
  }
  
  
 if (irq & MCP2515::CANINTF_RX1IF){
    mcp2515.readMessage(MCP2515::RXB1, &canMsg);
    Serial.print(canMsg.can_id, HEX); 
    Serial.print(" ");
    Serial.print(canMsg.can_id & CAN_EFF_MASK, HEX); 
    Serial.print(" "); 
    Serial.print(canMsg.can_dlc, HEX); 
    Serial.print(" ");   
    for (int i = 0; i<canMsg.can_dlc; i++){  
      Serial.print(canMsg.data[i],HEX);
      Serial.print(" ");
    }
    Serial.println();   
  }
  
  if (!irq){
    //Serial.print("No irq.");
    //Serial.println();
  }

  //msg.can_id &= CAN_EFF_MASK;
  

  //delay(1000);
 
}
