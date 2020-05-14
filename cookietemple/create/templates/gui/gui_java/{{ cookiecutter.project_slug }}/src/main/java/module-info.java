module {{ cookiecutter.project_slug }} {
    requires javafx.controls;
    requires javafx.fxml;

    opens org.{{ cookiecutter.organization }} to javafx.fxml;
    exports org.{{ cookiecutter.organization }};
}
