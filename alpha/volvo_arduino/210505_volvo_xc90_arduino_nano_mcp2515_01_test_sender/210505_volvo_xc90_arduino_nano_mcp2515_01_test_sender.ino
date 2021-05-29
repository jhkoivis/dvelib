
// use CH340 usb-serial-drivers

// Tools->board->arduino AVR boards->arduino nano
// Tools->processor->atmega328P (old bootloader)

#include <stdio.h>
#include <mcp2515.h>      //Library for using CAN Communication

// https://github.com/olegel/VolvoCan


///////////////////////////////////////////////////////////////
// Initialize variables
///////////////////////////////////////////////////////////////
struct can_frame canMsg;
MCP2515 mcp2515(10);
char printBuffer80[80];
int ig;

namespace GearBox
{
enum Enum
{
    Unknown           = 0,
    Parking           = 1,
    Rear              = 2,
    Neutral           = 3,
    Drive             = 4,
    DrivingRear       = 7,
    DrivingNeutral    = 0
};
}

struct CCarState
{
    static const uint8_t MaxParkingDistance = 0x1F;

    GearBox::Enum   _gear                   = GearBox::Unknown;
    GearBox::Enum   _drivingGear            = GearBox::Unknown;
    bool            _parkingAssistance      = true;
    bool            _parkingButtonPressed   = false;
    uint8_t         _lightMeter             = 0;
    bool            _keyInLock              = false;
    uint8_t         _keyPosition            = 0;

    uint8_t         _parkingDistance        = MaxParkingDistance;
    uint16_t        _wheelButtons           = 0;
};

CCarState carState;

static const unsigned long GearBoxId        = 0x3003028;
static const unsigned long CcmId            = 0xE00442;
static const unsigned long RemId            = 0x1E0522E;
static const unsigned long CemId            = 0x617FF8;
static const unsigned long SwmId            = 0x404066;

///////////////////////////////////////////////////////////////

void PrintMessage(can_frame &msg)
    {
        Serial.print(msg.can_id & CAN_EFF_MASK, HEX); // print ID
        Serial.print(" "); 
        Serial.print(msg.can_dlc, HEX); // print DLC
        Serial.print(" ");
        
        for (int i = 0; i<msg.can_dlc; i++)  {  // print the data
            
        Serial.print(msg.data[i],HEX);
        Serial.print(" ");

        }

        Serial.println();      
    }


void ProcessMessage(can_frame &msg, CCarState &carState)
    {
        msg.can_id &= CAN_EFF_MASK;

        PrintMessage(msg);

        switch(msg.can_id)
        {
            case GearBoxId:
            {
                GearBox::Enum gear = (GearBox::Enum)(msg.data[2] & 0x7);
                if( carState._gear != gear )
                {
                    carState._gear = gear;
                    Serial.print("Gear ");
                    Serial.println(carState._gear);
                }
                gear = (GearBox::Enum)((msg.data[2] & 0x70) >> 5);
                if( carState._drivingGear != gear )
                {
                    carState._drivingGear = gear;
                    Serial.print("Gear2 ");
                    Serial.println(carState._drivingGear);
                }
                break;
            }
            case CcmId:
            {
                bool parkingButtonPressed = (msg.data[2] & 0x40) > 0;

                if(parkingButtonPressed != carState._parkingButtonPressed)
                {
                    carState._parkingButtonPressed = parkingButtonPressed;
                    if(parkingButtonPressed)
                        carState._parkingAssistance = ! carState._parkingAssistance;

                    Serial.print("ParkButton ");
                    Serial.println(parkingButtonPressed);
                    Serial.print(" enabled ");
                    Serial.println(carState._parkingAssistance);
                }

                uint8_t light = msg.data[3] & 0xF;
                if( carState._lightMeter != light )
                {
                    carState._lightMeter = light;
                    Serial.print("LightMeter ");
                    Serial.println(carState._lightMeter);
                }
                break;
            }
            case RemId:
            {
                uint8_t distance = CCarState::MaxParkingDistance - (msg.data[3] >> 3);
                //uint8_t distance = msg.data[3] >> 3;
                if( carState._parkingDistance != distance )
                {
                    carState._parkingDistance = distance;
                    Serial.print("Distance ");
                    Serial.println(carState._parkingDistance);
                }
                break;
            }
            case CemId:
            {
                uint8_t keyPosition = msg.data[6] >> 5;
                bool key = (keyPosition & 0x4) > 0;
                if( carState._keyInLock != key )
                {
                    carState._keyInLock = key;
                    Serial.print("Key ");
                    Serial.println(carState._keyInLock);
                }
                keyPosition = keyPosition & 0x3;
                if( carState._keyPosition != keyPosition )
                {
                    carState._keyPosition = keyPosition;
                    Serial.print("Key pos ");
                    Serial.println(carState._keyPosition);
                }
                break;
            }
            case SwmId:
            {
                uint16_t buttons = msg.data[6] & 0x3F;
                buttons = (buttons<<8) | ((~msg.data[7]) & 0x3F);
                if( carState._wheelButtons != buttons )
                {
                    carState._wheelButtons = buttons;
                    Serial.print("Buttons ");
                    Serial.println(carState._wheelButtons, HEX);
                }
                break;
            }
            default:
                //PrintMessage(msg);
                break;
        }
    }

///////////////////////////////////////////////////////////////
// Setup
///////////////////////////////////////////////////////////////
void setup() 
{

  ig=3;
  
  ////////////////////////////////////////////////////////////
  // Init serial
  ////////////////////////////////////////////////////////////
  Serial.begin(9600);
  while (!Serial);  // wait for serial to open...
  sprintf(        printBuffer80, "[%010d] Serial started\n", millis());
  Serial.print(   printBuffer80);
  ////////////////////////////////////////////////////////////



  ////////////////////////////////////////////////////////////
  // Init MCP2515
  /////////////////////////////////////////////////////////////
  if (MCP2515::ERROR_OK !=                          mcp2515.reset()) {
    sprintf(      printBuffer80,  "[%010d] Failure: mcp2515.reset()\n", millis());
    Serial.print( printBuffer80);
  } else{
    sprintf(      printBuffer80,  "[%010d] Success: mcp2515.reset()\n", millis());
    Serial.print( printBuffer80);
  }

  
  if ( MCP2515::ERROR_OK !=                         mcp2515.setBitrate( CAN_125KBPS, MCP_8MHZ)){
    sprintf(      printBuffer80,  "[%010d] Failure: mcp2515.setBitrate( CAN_125KBPS, MCP_8MHZ)\n", millis());
    Serial.print( printBuffer80);
  } else{
    sprintf(      printBuffer80,  "[%010d] Success: mcp2515.setBitrate( CAN_125KBPS, MCP_8MHZ)\n", millis());
    Serial.print( printBuffer80);
  }
  
  // alternative: mcp2515.setNormalMode();
  if ( MCP2515::ERROR_OK !=                         mcp2515.setNormalMode()) {
    sprintf(      printBuffer80,  "[%010d] Failure: mcp2515.setNormalMode()\n", millis());
    Serial.print( printBuffer80);
  } else{
    sprintf(      printBuffer80,  "[%010d] Success: mcp2515.setNormalMode()\n", millis());
    Serial.print( printBuffer80);
  }
  ////////////////////////////////////////////////////////////////////////////////////////
  
}

void loop() 
{
  sprintf(      printBuffer80,  "[%010ld] Startin loop number: %04d\n", millis(), ig);
  Serial.print( printBuffer80);
  //Serial.print(ig);
  ig = ig+1;
 
  canMsg.can_id  = GearBoxId;       //CAN id as 0x036
  canMsg.can_dlc = 8;               //CAN data length as 8
  canMsg.data[0] = 1;               //Update humidity value in [0]
  canMsg.data[1] = 2;               //Update temperature value in [1]
  canMsg.data[2] = ig;               //Rest all with 0
  canMsg.data[3] = 0x00;
  canMsg.data[4] = 0x00;
  canMsg.data[5] = 0x00;
  canMsg.data[6] = 0x00;
  canMsg.data[7] = 0x00;
  mcp2515.sendMessage(&canMsg);     //Sends the CAN message

  PrintMessage(canMsg);
  
  delay(1000);
}
