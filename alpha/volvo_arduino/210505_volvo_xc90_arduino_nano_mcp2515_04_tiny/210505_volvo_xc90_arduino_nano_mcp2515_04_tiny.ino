
#include <mcp2515.h>   

// volume up/down ???
// 10 8131726C 131726C 8 0 8C 4C D2 E0 40 0 37
// 9  8131726C 131726C 8 0 8C 4E D2 E0 40 0 37

// off/parking/low beams ???
// 217FFC 8 7 EB 40 D2 F0 58 0 0 
// 217FFC 8 7 EB 40 D4 F0 58 0 0 
// 217FFC 8 7 EB 40 D8 F0 58 0 0 
// 217FFC 8 7 EB 40 D4 F0 58 0 0

// DEM, Door open ???
// 14034A2 8 0 5B 40 4 89 23 4 0 


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
    /*
    if (canMsg.can_id == 0x8131726C) 
    {
      Serial.print("\n---------------------------------------------\n");
    
      if (canMsg.data[7] == 0x37) {
        // 16:20:48.976 -> 8131726C 131726C 8 0 8C 91 D2 E0 40 0 37
        Serial.print("\nVolume up\n");
        Serial.print("\n---------------------------------------------\n");
      }
      
      if (canMsg.data[7] == 0x3b){
        // 16:21:17.497 -> 8131726C 131726C 8 0 8C 95 D2 E0 40 0 3B 
        Serial.print("\nVolume down\n");
        Serial.print("\n---------------------------------------------\n");
      }

      if (canMsg.data[7] == 0x3d){
        // 16:21:36.025 -> 8131726C 131726C 8 0 8C 8E D2 E0 40 0 3D
        Serial.print("\n next track\n");
        Serial.print("\n---------------------------------------------\n");
      }

      if (canMsg.data[7] == 0x3e){
        // 16:23:38.398 -> 8131726C 131726C 8 0 8C 93 D2 E0 40 0 3E 
        Serial.print("\n previous track\n");
        Serial.print("\n---------------------------------------------\n");
      }


    }
    */
    if (canMsg.can_id == 0x80217FFC) 
    {
      Serial.print("\n---------------------------------------------\n");
    
      if (canMsg.data[3] == 0xd2) {
        // 16:29:27.298 -> 80217FFC 217FFC 8 5 6B 40 D2 F0 58 0 0 
        Serial.print("\n Lights off\n");
        Serial.print("\n---------------------------------------------\n");
      }

      if (canMsg.data[3] == 0xd4) {
        // 16:29:27.298 -> 80217FFC 217FFC 8 5 6B 40 D2 F0 58 0 0 
        Serial.print("\n Lights: park on \n");
        Serial.print("\n---------------------------------------------\n");
      }

      if (canMsg.data[3] == 0xd8) {
        // 16:29:27.298 -> 80217FFC 217FFC 8 5 6B 40 D2 F0 58 0 0 
        Serial.print("\n Lights: low beams \n");
        Serial.print("\n---------------------------------------------\n");
      }
      
    
    
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
  }
  
  
 if (irq & MCP2515::CANINTF_RX1IF){
    mcp2515.readMessage(MCP2515::RXB1, &canMsg);
    if (canMsg.can_id == 0x8131726C) 
    {
      Serial.print("\n---------------------------------------------\n");
    
      if (canMsg.data[7] == 0x37) 
        Serial.print("\nVolume up\n");
        Serial.print("\n---------------------------------------------\n");

         if (canMsg.data[7] == 0x3b) 
        Serial.print("\nVolume down\n");
        Serial.print("\n---------------------------------------------\n");
    
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
  }
  
  if (!irq){
    //Serial.print("No irq.");
    //Serial.println();
  }

  //msg.can_id &= CAN_EFF_MASK;
  

  //delay(1000);
 
}
