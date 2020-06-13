package {{ cookiecutter.group_domain }}.{{ cookiecutter.group_organization }};

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;

import java.io.File;
import java.io.IOException;
import java.util.concurrent.TimeUnit;

import static org.junit.jupiter.api.Assertions.assertEquals;

class {{ cookiecutter.main_class }}ImageTest {

    @Tag("native-image")
    @Test
    public void testUsageHelp() throws IOException, InterruptedException {
        Process process = new ProcessBuilder(NativeImageHelper.executable(), "--help").start();

        String expected = String.format("" +
                "Usage: {{ cookiecutter.project_slug }} [-hV] [-a=<algorithm>] [@<filename>...] <file>%n" +
                "Prints the checksum (MD5 by default) of a file to STDOUT.%n" +
                "      [@<filename>...]   One or more argument files containing options.%n" +
                "      <file>             The file whose checksum to calculate, or '-' to read%n" +
                "                           from the standard input stream.%n" +
                "  -a, --algorithm=<algorithm>%n" +
                "                         MD5, SHA-1, SHA-256, ...%n" +
                "  -h, --help             Show this help message and exit.%n" +
                "  -V, --version          Print version information and exit.%n");
        Assertions.assertEquals(expected, NativeImageHelper.getStdOut(process));
        Assertions.assertEquals("", NativeImageHelper.getStdErr(process));
        process.waitFor(3, TimeUnit.SECONDS);
        assertEquals(0, process.exitValue());
        process.destroyForcibly();
    }

    @Tag("native-image")
    @Test
    public void testVersionInfo() throws IOException, InterruptedException {
        Process process = new ProcessBuilder(NativeImageHelper.executable(), "--version").start();

        String expected = String.format("{{ cookiecutter.project_slug }} 4.0%n"); // JVM: 1.8.0_222 (Oracle Corporation Substrate VM GraalVM dev)

        Assertions.assertEquals(expected, NativeImageHelper.getStdOut(process));
        Assertions.assertEquals("", NativeImageHelper.getStdErr(process));
        process.waitFor(3, TimeUnit.SECONDS);
        assertEquals(0, process.exitValue());
        process.destroyForcibly();
    }

    @Tag("native-image")
    @Test
    public void testDefaultAlgorithm() throws IOException, InterruptedException {
        File tempFile = NativeImageHelper.createTempDataFile();

        Process process = new ProcessBuilder(NativeImageHelper.executable(), tempFile.getAbsolutePath()).start();

        String expected = String.format("764efa883dda1e11db47671c4a3bbd9e%n");

        Assertions.assertEquals("", NativeImageHelper.getStdErr(process));
        Assertions.assertEquals(expected, NativeImageHelper.getStdOut(process));
        process.waitFor(3, TimeUnit.SECONDS);
        assertEquals(0, process.exitValue());
        tempFile.delete();
        process.destroyForcibly();
    }

    @Tag("native-image")
    @Test
    public void testMd5Algorithm() throws IOException, InterruptedException {
        File tempFile = NativeImageHelper.createTempDataFile();

        Process process = new ProcessBuilder(NativeImageHelper.executable(), "-a", "md5", tempFile.getAbsolutePath()).start();

        String expected = String.format("764efa883dda1e11db47671c4a3bbd9e%n");

        Assertions.assertEquals(expected, NativeImageHelper.getStdOut(process));
        Assertions.assertEquals("", NativeImageHelper.getStdErr(process));
        process.waitFor(3, TimeUnit.SECONDS);
        assertEquals(0, process.exitValue());
        tempFile.delete();
        process.destroyForcibly();
    }

    @Tag("native-image")
    @Test
    public void testSha1Algorithm() throws IOException, InterruptedException {
        File tempFile = NativeImageHelper.createTempDataFile();

        Process process = new ProcessBuilder(NativeImageHelper.executable(), "-a", "sha1", tempFile.getAbsolutePath()).start();

        String expected = String.format("55ca6286e3e4f4fba5d0448333fa99fc5a404a73%n");

        Assertions.assertEquals(expected, NativeImageHelper.getStdOut(process));
        Assertions.assertEquals("", NativeImageHelper.getStdErr(process));
        process.waitFor(3, TimeUnit.SECONDS);
        assertEquals(0, process.exitValue());
        tempFile.delete();
        process.destroyForcibly();
    }

    @Tag("native-image")
    @Test
    public void testInvalidInput_MissingRequiredArg() throws IOException, InterruptedException {
        Process process = new ProcessBuilder(NativeImageHelper.executable()).start();

        String expected = String.format("" +
                "Missing required parameter: '<file>'%n" +
                "Usage: {{ cookiecutter.project_slug }} [-hV] [-a=<algorithm>] [@<filename>...] <file>%n" +
                "Prints the checksum (MD5 by default) of a file to STDOUT.%n" +
                "      [@<filename>...]   One or more argument files containing options.%n" +
                "      <file>             The file whose checksum to calculate, or '-' to read%n" +
                "                           from the standard input stream.%n" +
                "  -a, --algorithm=<algorithm>%n" +
                "                         MD5, SHA-1, SHA-256, ...%n" +
                "  -h, --help             Show this help message and exit.%n" +
                "  -V, --version          Print version information and exit.%n");
        Assertions.assertEquals(expected, NativeImageHelper.getStdErr(process));
        Assertions.assertEquals("", NativeImageHelper.getStdOut(process));
        process.waitFor(3, TimeUnit.SECONDS);
        assertEquals(2, process.exitValue());
        process.destroyForcibly();
    }

    @Tag("native-image")
    @Test
    public void testInvalidInput_UnknownOption() throws IOException, InterruptedException {
        Process process = new ProcessBuilder(NativeImageHelper.executable(), "file", "--unknown").start();

        String expected = String.format("" +
                "Unknown option: '--unknown'%n" +
                "Usage: {{ cookiecutter.project_slug }} [-hV] [-a=<algorithm>] [@<filename>...] <file>%n" +
                "Prints the checksum (MD5 by default) of a file to STDOUT.%n" +
                "      [@<filename>...]   One or more argument files containing options.%n" +
                "      <file>             The file whose checksum to calculate, or '-' to read%n" +
                "                           from the standard input stream.%n" +
                "  -a, --algorithm=<algorithm>%n" +
                "                         MD5, SHA-1, SHA-256, ...%n" +
                "  -h, --help             Show this help message and exit.%n" +
                "  -V, --version          Print version information and exit.%n");
        Assertions.assertEquals(expected, NativeImageHelper.getStdErr(process));
        Assertions.assertEquals("", NativeImageHelper.getStdOut(process));
        process.waitFor(3, TimeUnit.SECONDS);
        assertEquals(2, process.exitValue());
        process.destroyForcibly();
    }

}
