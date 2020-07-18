package {{ cookiecutter.group_domain }}.{{ cookiecutter.group_organization }};

import picocli.CommandLine;
import picocli.CommandLine.Command;
import picocli.CommandLine.Option;
import picocli.CommandLine.Parameters;
import picocli.jansi.graalvm.AnsiConsole;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.math.BigInteger;
import java.nio.file.Files;
import java.security.MessageDigest;
import java.util.concurrent.Callable;

@Command(name = "{{ cookiecutter.project_slug }}", mixinStandardHelpOptions = true, showAtFileInUsageHelp = true,
        version = "{{ cookiecutter.project_slug }} 4.0",
        description = "Prints the checksum (MD5 by default) of a file to STDOUT.")
class {{ cookiecutter.main_class }} implements Callable<Integer> {

    @Parameters(index = "0", description = "The file whose checksum to calculate, or '-' to read from the standard input stream.")
    private File file;

    @Option(names = {"-a", "--algorithm"}, description = "MD5, SHA-1, SHA-256, ...")
    private String algorithm = "MD5";

    public static void main(String... args) {
        int exitCode;
        try (AnsiConsole ansi = AnsiConsole.windowsInstall()) {
            exitCode = new CommandLine(new {{ cookiecutter.main_class }}()).execute(args);
        }
        System.exit(exitCode);
    }

    @Override
    public Integer call() throws Exception { // your business logic goes here...
        byte[] fileContents = "-".equals(file.getName())
                ? readFully(System.in) : Files.readAllBytes(file.toPath());
        byte[] digest = MessageDigest.getInstance(algorithm).digest(fileContents);
        System.out.printf("%0" + (digest.length * 2) + "x%n", new BigInteger(1, digest));
        return 0;
    }

    private byte[] readFully(InputStream is) throws IOException {
        ByteArrayOutputStream buffer = new ByteArrayOutputStream();
        int nRead;
        byte[] data = new byte[1024];
        while ((nRead = is.read(data, 0, data.length)) != -1) {
            buffer.write(data, 0, nRead);
        }

        buffer.flush();
        return buffer.toByteArray();
    }
}
