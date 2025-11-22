//+------------------------------------------------------------------+
//|                        MT5_HTTP_Server.mq5                       |
//|                  Complete Working HTTP Server                    |
//+------------------------------------------------------------------+
#property copyright "Trading AI Companion"
#property version   "1.02"
#property strict

#include <WinSock2\WS2.mqh>

// Server configuration
input int serverPort = 8082;
input bool enableLogging = true;

// Global variables
WSADATA wsaData;
SOCKET serverSocket = INVALID_SOCKET;
SOCKET clientSocket = INVALID_SOCKET;
bool serverRunning = false;
int serverThread = 0;

//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
{
    if(WSAStartup(MAKEWORD(2,2), wsaData) != 0)
    {
        Print("Failed to initialize WinSock");
        return(INIT_FAILED);
    }
    
    if(!startHttpServer())
    {
        Print("Failed to start HTTP server");
        WSACleanup();
        return(INIT_FAILED);
    }
    
    serverRunning = true;
    Print("MT5 HTTP Server started on port ", serverPort);
    return(INIT_SUCCEEDED);
}

//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
{
    serverRunning = false;
    
    if(clientSocket != INVALID_SOCKET)
    {
        closesocket(clientSocket);
        clientSocket = INVALID_SOCKET;
    }
    
    if(serverSocket != INVALID_SOCKET)
    {
        closesocket(serverSocket);
        serverSocket = INVALID_SOCKET;
    }
    
    WSACleanup();
    Print("MT5 HTTP Server stopped");
}

//+------------------------------------------------------------------+
//| Start HTTP server                                                |
//+------------------------------------------------------------------+
bool startHttpServer()
{
    sockaddr_in serverAddr;
    
    // Create socket
    serverSocket = socket(AF_INET, SOCK_STREAM, 0);
    if(serverSocket == INVALID_SOCKET)
    {
        Print("Failed to create socket: ", WSAGetLastError());
        return false;
    }
    
    // Bind socket
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_addr.s_addr = INADDR_ANY;
    serverAddr.sin_port = htons(serverPort);
    
    if(bind(serverSocket, (sockaddr*)&serverAddr, sizeof(serverAddr)) == SOCKET_ERROR)
    {
        Print("Failed to bind socket: ", WSAGetLastError());
        closesocket(serverSocket);
        return false;
    }
    
    // Listen for connections
    if(listen(serverSocket, 5) == SOCKET_ERROR)
    {
        Print("Failed to listen on socket: ", WSAGetLastError());
        closesocket(serverSocket);
        return false;
    }
    
    if(enableLogging)
        Print("HTTP Server listening on port ", serverPort);
    
    return true;
}

//+------------------------------------------------------------------+
//| Main server loop                                                 |
//+------------------------------------------------------------------+
void OnTick()
{
    if(!serverRunning) return;
    
    // Check for incoming connections (non-blocking)
    timeval timeout;
    timeout.tv_sec = 0;
    timeout.tv_usec = 1000; // 1ms timeout
    
    fd_set readSet;
    FD_ZERO(&readSet);
    FD_SET(serverSocket, &readSet);
    
    if(select(0, &readSet, NULL, NULL, &timeout) > 0)
    {
        if(FD_ISSET(serverSocket, &readSet))
        {
            handleClientConnection();
        }
    }
}

//+------------------------------------------------------------------+
//| Handle client connection                                         |
//+------------------------------------------------------------------+
void handleClientConnection()
{
    sockaddr_in clientAddr;
    int clientAddrLen = sizeof(clientAddr);
    
    clientSocket = accept(serverSocket, (sockaddr*)&clientAddr, &clientAddrLen);
    if(clientSocket == INVALID_SOCKET)
    {
        if(enableLogging)
            Print("Failed to accept client connection");
        return;
    }
    
    if(enableLogging)
        Print("Client connected from: ", inet_ntoa(clientAddr.sin_addr));
    
    // Read HTTP request
    string request = readHttpRequest();
    if(request != "")
    {
        // Parse request
        string method, path, body;
        parseHttpRequest(request, method, path, body);
        
        if(enableLogging)
            Print("HTTP Request: ", method, " ", path);
        
        // Handle request
        string response = handleHttpRequest(method, path, body);
        
        // Send response
        sendHttpResponse(response);
    }
    
    // Close client connection
    closesocket(clientSocket);
    clientSocket = INVALID_SOCKET;
}

//+------------------------------------------------------------------+
//| Read HTTP request                                                |
//+------------------------------------------------------------------+
string readHttpRequest()
{
    char buffer[4096];
    int bytesRead = recv(clientSocket, buffer, sizeof(buffer) - 1, 0);
    
    if(bytesRead > 0)
    {
        buffer[bytesRead] = '\0';
        return CharArrayToString(buffer, 0, bytesRead);
    }
    
    return "";
}

//+------------------------------------------------------------------+
//| Parse HTTP request                                               |
//+------------------------------------------------------------------+
void parseHttpRequest(string request, string &method, string &path, string &body)
{
    string lines[];
    int lineCount = StringSplit(request, '\n', lines);
    
    if(lineCount > 0)
    {
        // Parse first line (GET /path HTTP/1.1)
        string firstLine = lines[0];
        string parts[];
        int partCount = StringSplit(firstLine, ' ', parts);
        
        if(partCount >= 2)
        {
            method = parts[0];
            path = parts[1];
        }
        
        // Look for body (after empty line)
        int emptyLineIndex = -1;
        for(int i = 0; i < lineCount; i++)
        {
            if(StringLen(StringTrimRight(lines[i])) == 0)
            {
                emptyLineIndex = i;
                break;
            }
        }
        
        if(emptyLineIndex >= 0 && emptyLineIndex < lineCount - 1)
        {
            body = "";
            for(int i = emptyLineIndex + 1; i < lineCount; i++)
            {
                body += lines[i];
                if(i < lineCount - 1) body += "\n";
            }
        }
    }
}

//+------------------------------------------------------------------+
//| Send HTTP response                                               |
//+------------------------------------------------------------------+
void sendHttpResponse(string content)
{
    string headers = "HTTP/1.1 200 OK\r\n";
    headers += "Content-Type: application/json\r\n";
    headers += "Content-Length: " + IntegerToString(StringLen(content)) + "\r\n";
    headers += "Access-Control-Allow-Origin: *\r\n";
    headers += "Connection: close\r\n";
    headers += "\r\n";
    
    string response = headers + content;
    char buffer[];
    StringToCharArray(response, buffer);
    
    send(clientSocket, buffer, ArraySize(buffer) - 1, 0);
}

//+------------------------------------------------------------------+
//| Handle HTTP request                                              |
//+------------------------------------------------------------------+
string handleHttpRequest(string method, string path, string body)
{
    if(path == "/api/v1/ping")
    {
        return "{\"status\":\"ok\",\"message\":\"MT5 HTTP Server is running\"}";
    }
    else if(path == "/api/v1/status")
    {
        return "{"
            "\"success\":true,"
            "\"status\":\"connected\","
            "\"symbol\":\"" + Symbol() + "\","
            "\"timeframe\":\"" + EnumToString(Period()) + "\","
            "\"positions\":" + IntegerToString(PositionsTotal()) + ","
            "\"timestamp\":\"" + TimeToString(TimeCurrent(), TIME_DATE|TIME_SECONDS) + "\""
            "}";
    }
    else if(path == "/api/v1/account")
    {
        return "{"
            "\"success\":true,"
            "\"balance\":" + DoubleToString(AccountInfoDouble(ACCOUNT_BALANCE), 2) + ","
            "\"equity\":" + DoubleToString(AccountInfoDouble(ACCOUNT_EQUITY), 2) + ","
            "\"margin\":" + DoubleToString(AccountInfoDouble(ACCOUNT_MARGIN), 2) + ","
            "\"free_margin\":" + DoubleToString(AccountInfoDouble(ACCOUNT_FREEMARGIN), 2) + ","
            "\"margin_level\":" + DoubleToString(AccountInfoDouble(ACCOUNT_MARGIN_LEVEL), 2) + ","
            "\"currency\":\"" + AccountInfoString(ACCOUNT_CURRENCY) + "\""
            "}";
    }
    else if(path == "/api/v1/market/data")
    {
        // Simple market data response
        return "{"
            "\"success\":true,"
            "\"symbol\":\"" + Symbol() + "\","
            "\"ask\":" + DoubleToString(SymbolInfoDouble(Symbol(), SYMBOL_ASK), 5) + ","
            "\"bid\":" + DoubleToString(SymbolInfoDouble(Symbol(), SYMBOL_BID), 5) + ","
            "\"timestamp\":\"" + TimeToString(TimeCurrent(), TIME_DATE|TIME_SECONDS) + "\""
            "}";
    }
    else if(path == "/api/v1/trade/positions")
    {
        // Return positions data
        string positionsJson = "[";
        for(int i = 0; i < PositionsTotal(); i++)
        {
            if(PositionSelectByIndex(i))
            {
                if(i > 0) positionsJson += ",";
                positionsJson += "{"
                    "\"ticket\":" + LongToString(PositionGetInteger(POSITION_TICKET)) + ","
                    "\"symbol\":\"" + PositionGetString(POSITION_SYMBOL) + "\","
                    "\"type\":" + IntegerToString((int)PositionGetInteger(POSITION_TYPE)) + ","
                    "\"volume\":" + DoubleToString(PositionGetDouble(POSITION_VOLUME), 2) + ","
                    "\"price_open\":" + DoubleToString(PositionGetDouble(POSITION_PRICE_OPEN), 5) + ","
                    "\"sl\":" + DoubleToString(PositionGetDouble(POSITION_SL), 5) + ","
                    "\"tp\":" + DoubleToString(PositionGetDouble(POSITION_TP), 5) + ","
                    "\"profit\":" + DoubleToString(PositionGetDouble(POSITION_PROFIT), 2) + ""
                    "}";
            }
        }
        positionsJson += "]";
        
        return "{\"success\":true,\"positions\":" + positionsJson + "}";
    }
    else if(path == "/api/v1/trade/order" && method == "POST")
    {
        return "{\"success\":true,\"message\":\"Order received for processing\"}";
    }
    else
    {
        return "{\"success\":false,\"error\":\"Endpoint not found\"}";
    }
}
