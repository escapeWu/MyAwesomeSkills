# Java Organization Reference

Use this only when Java is present or the task explicitly adds Java code.
This repository currently has no Java module, so detect the build shape before
creating one.

## Detect The Build

```bash
rg --files | rg "(^|/)(pom.xml|build.gradle|settings.gradle|src/(main|test)/java/)"
```

If no Java build exists, do not introduce one casually. Ask whether Java is an
intended new runtime boundary unless the task explicitly requires it.

## Standard Layout

For Maven or Gradle projects, prefer the conventional layout:

```text
src/main/java/<base/package>/...
src/main/resources/...
src/test/java/<base/package>/...
src/test/resources/...
```

Keep tests in the same package path as the class under test.

## Package Boundaries

- Use reverse-DNS base packages when a project already has a domain name, then
  organize by bounded context.
- Prefer domain-first packages, with layer folders inside the domain when
  needed:

```text
com.example.tradingsignal.evaluation.api
com.example.tradingsignal.evaluation.application
com.example.tradingsignal.evaluation.domain
com.example.tradingsignal.evaluation.infrastructure
```

- Avoid top-level `controller`, `service`, `repository` packages that mix
  unrelated domains. They make context grep harder as the codebase grows.
- Do not create `util` as a dumping ground. Shared helpers should have narrow
  names such as `time`, `money`, `json`, or stay domain-local.

## Spring-Style Guidance

If the Java module uses Spring:

- Controllers are HTTP adapters and should stay thin.
- Application services own use-case orchestration and transactions.
- Domain classes own validation and business invariants where practical.
- Repository interfaces/adapters own persistence details.
- DTOs are API contracts; entities are persistence/domain contracts. Do not
  leak entities as public API responses by default.

## Naming And Tests

- Classes use `UpperCamelCase`; methods and fields use `lowerCamelCase`.
- Package names are lowercase.
- Unit tests mirror package names and usually end with `Test`.
- Integration tests should have a distinct suffix such as `IT` only if the
  build is configured for it.

## Grep Flow

```bash
rg -n "class Evaluation|interface Evaluation|@RestController|@Service|@Repository" src/main/java src/test/java
rg -n "EvaluationRequest|EvaluationResponse|EvaluationEntity|EvaluationRepository" src/main/java src/test/java
```

When adding a feature, trace request DTO, controller, application service,
domain model, repository adapter, and tests before creating new packages.

## Primary References

- Oracle Java naming conventions:
  https://www.oracle.com/java/technologies/javase/codeconventions-namingconventions.html
- Spring Boot structuring code:
  https://docs.spring.io/spring-boot/reference/using/structuring-your-code.html
