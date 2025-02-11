//+------------------------------------------------------------------+
//|                                       CodeLocus_IG sentiment.mq5 |
//|                        Copyright 2018, MetaQuotes Software Corp. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2018, MetaQuotes Software Corp."
#property link      "https://www.mql5.com"
#property version   "1.00"
#property indicator_separate_window
#property indicator_buffers 1
#property indicator_plots 1
#property indicator_type1   DRAW_SECTION
#property indicator_color1  clrGreen
#property indicator_width1 2
/*#property indicator_type2   DRAW_LINE
#property indicator_color2  clrDarkBlue
#property indicator_width2 1
#property indicator_type3   DRAW_LINE
#property indicator_color3  clrDarkRed
#property indicator_width3 1*/
 bool invert       =false;//Invert Data
input bool checkEurusd = true;//EurUsd
input bool checkGbpusd = false;//GbpUsd
input bool checkUsdjpy = false;//UsdJpy
input bool checkAudusd = false;//AUDUSD
input bool checkGold = false;//GOLD



//input bool minmax      = false;//Min/Max

double output[];
/*double max[];
double min[];*/
datetime last;
void OnDeinit(const int reson)
   {
   ObjectDelete(0,"CL_Button");
   }
int OnInit()
  {
   IndicatorSetString(INDICATOR_SHORTNAME,"-");
//--- indicator buffers mapping
   int drawbegin;
   drawbegin = iBars(_Symbol,PERIOD_CURRENT)-iBarShift(_Symbol,PERIOD_CURRENT,D'2018.12.17 00:20');
   
  // PlotIndexSetInteger(0,PLOT_SHIFT,-1);
   SetIndexBuffer(0,output,INDICATOR_DATA);
   PlotIndexSetInteger(0,PLOT_DRAW_BEGIN,drawbegin);
   PlotIndexSetDouble(0,PLOT_EMPTY_VALUE,0.0);
   //PlotIndexSetDouble(0,PLOT_EMPTY_VALUE,100.0);
   ArraySetAsSeries(output,true);
   ButtonCreate();
   /*if(minmax)
      {
      SetIndexBuffer(1,max,INDICATOR_DATA);
      PlotIndexSetInteger(1,PLOT_DRAW_BEGIN,drawbegin);
      ArraySetAsSeries(max,true);
      SetIndexBuffer(2,min,INDICATOR_DATA);
      PlotIndexSetInteger(2,PLOT_DRAW_BEGIN,drawbegin);
      ArraySetAsSeries(min,true);
      }*/
      
 
  
   
   
   return(INIT_SUCCEEDED);
  }
//+------------------------------------------------------------------+
//| Custom indicator iteration function                              |
//+------------------------------------------------------------------+
int OnCalculate(const int rates_total,
                const int prev_calculated,
                const datetime &time[],
                const double &open[],
                const double &high[],
                const double &low[],
                const double &close[],
                const long &tick_volume[],
                const long &volume[],
                const int &spread[])
  {
//---

   if(newCandle()&&!buttonState())
      {
      
      ArrayInitialize(output,0);
      int barSh;
      double sentiment;
      int handle = FileOpen("CL_OANDA_Sentiment\\Rutime_data.csv",FILE_ANSI|FILE_READ,",");
      int i=0;
      FileReadString(handle);
      FileReadString(handle);
      FileReadString(handle);
      FileReadString(handle);
      FileReadString(handle);
      FileReadString(handle);
    
      while(!FileIsEnding(handle))
         {
         if(i%6==0)
            {
            barSh=iBarShift(_Symbol,PERIOD_CURRENT,datetime(FileReadString(handle))-datetime(1200));
            i++;
            }
         if(i%6==1&&checkEurusd)
            {
            sentiment = double(FileReadString(handle));
            i++;
            }
         if(i%6==2&&checkGbpusd)
            {
            sentiment = double(FileReadString(handle));
            i++;
            }
         if(i%6==3&&checkUsdjpy)
            {
            sentiment = double(FileReadString(handle));
            i++;
            }
         if(i%6==4&&checkAudusd)
            {
            
            sentiment = double(FileReadString(handle));
            
            i++;
            }
         if(i%6==5&&checkGold)
            {
            sentiment = double(FileReadString(handle));
            i++;
            }
         else 
            {
            FileReadString(handle);
            i++;
            }
        
         if(invert)output[barSh]=-sentiment;
         else output[barSh]=sentiment;
         /*if(minmax)
            {
            if(max[barSh]==0)max[barSh]=sentiment;
            if(min[barSh]==0)min[barSh]=sentiment;
            if(sentiment>max[barSh])max[barSh]=sentiment;
            if(sentiment<min[barSh])min[barSh]=sentiment;
            }*/
         
         }
      
      FileClose(handle);
      int drawbegin = iBars(_Symbol,PERIOD_CURRENT)-iBarShift(_Symbol,PERIOD_CURRENT,D'2018.12.04 08:00');
      for(int j=drawbegin;j>=0;j--)
         {
         if(output[j]==0)output[j]=output[j+1];
         }
      
         
      }   
   if(buttonState())
      {
      int drawbegin = iBars(_Symbol,PERIOD_CURRENT)-iBarShift(_Symbol,PERIOD_CURRENT,D'2018.12.04 08:00');
      for(int j=drawbegin+10;j>=0;j--)
         {
         output[j]=EMPTY_VALUE;
         } 
      }
      
//--- return value of prev_calculated for next call
   return(rates_total);
   
  }
//+------------------------------------------------------------------+
bool newCandle()
   {
   datetime tim = iTime(_Symbol,PERIOD_CURRENT,0);
   if(TimeCurrent()>=datetime(tim)+13)
      {
      if(tim!=last)
      {
      last=tim;
      return true;
      }
      else return false;
      }
   return false;
   }
   
bool ButtonCreate(const long              chart_ID=0,               // chart's ID 
                  const string            name="CL_Button",            // button name 
                  const int               sub_window=1,             // subwindow index 
                  const int               x=60,                      // X coordinate 
                  const int               y=10,                      // Y coordinate 
                  const int               width=50,                 // button width 
                  const int               height=18,                // button height 
                  const ENUM_BASE_CORNER  corner=CORNER_RIGHT_UPPER, // chart corner for anchoring 
                  const string            text="Hide",            // text 
                  const string            font="Arial",             // font 
                  const int               font_size=10,             // font size 
                  const color             clr=clrBlack,             // text color 
                  const color             back_clr=clrLightGreen,  // background color 
                  const color             border_clr=clrNONE,       // border color 
                  const bool              state=false,              // pressed/released 
                  const bool              back=false,               // in the background 
                  const bool              selection=false,          // highlight to move 
                  const bool              hidden=true,              // hidden in the object list 
                  const long              z_order=0)                // priority for mouse click 
  { 
//--- reset the error value 
   ResetLastError(); 
//--- create the button 
   if(!ObjectCreate(chart_ID,name,OBJ_BUTTON,sub_window,0,0)) 
     { 
      Print(__FUNCTION__, 
            ": failed to create the button! Error code = ",GetLastError()); 
      return(false); 
     } 
//--- set button coordinates 
   ObjectSetInteger(chart_ID,name,OBJPROP_XDISTANCE,x); 
   ObjectSetInteger(chart_ID,name,OBJPROP_YDISTANCE,y); 
//--- set button size 
   ObjectSetInteger(chart_ID,name,OBJPROP_XSIZE,width); 
   ObjectSetInteger(chart_ID,name,OBJPROP_YSIZE,height); 
//--- set the chart's corner, relative to which point coordinates are defined 
   ObjectSetInteger(chart_ID,name,OBJPROP_CORNER,corner); 
//--- set the text 
   ObjectSetString(chart_ID,name,OBJPROP_TEXT,text); 
//--- set text font 
   ObjectSetString(chart_ID,name,OBJPROP_FONT,font); 
//--- set font size 
   ObjectSetInteger(chart_ID,name,OBJPROP_FONTSIZE,font_size); 
   
//--- set text color 
   ObjectSetInteger(chart_ID,name,OBJPROP_COLOR,clr); 
//--- set background color 
   ObjectSetInteger(chart_ID,name,OBJPROP_BGCOLOR,back_clr); 
//--- set border color 
   ObjectSetInteger(chart_ID,name,OBJPROP_BORDER_COLOR,border_clr); 
//--- display in the foreground (false) or background (true) 
   ObjectSetInteger(chart_ID,name,OBJPROP_BACK,back); 
//--- set button state 
   ObjectSetInteger(chart_ID,name,OBJPROP_STATE,state); 
//--- enable (true) or disable (false) the mode of moving the button by mouse 
   ObjectSetInteger(chart_ID,name,OBJPROP_SELECTABLE,selection); 
   ObjectSetInteger(chart_ID,name,OBJPROP_SELECTED,selection); 
//--- hide (true) or display (false) graphical object name in the object list 
   ObjectSetInteger(chart_ID,name,OBJPROP_HIDDEN,hidden); 
//--- set the priority for receiving the event of a mouse click in the chart 
   ObjectSetInteger(chart_ID,name,OBJPROP_ZORDER,z_order); 
//--- successful execution 
   return(true); 
  }
  
bool buttonState()
   {
   return false;//ObjectGetInteger(0,"CL_Button",OBJPROP_STATE);
   }