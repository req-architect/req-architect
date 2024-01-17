describe("User journey", () => {
    it("should navigate to github page", () => {
        cy.visit("http://localhost:3000/");
        cy.contains("Welcome");
        cy.get('button:contains("Login with GitHub")')
            .click()
            .then(() => {
                cy.location("href").should(
                    "include",
                    "https://github.com/login?",
                );
            });
    });

    it("should navigate to gitlab page", () => {
        cy.visit("http://localhost:3000/");
        cy.get('button:contains("Login with GitLab")')
            .click()
            .then(() => {
                cy.location("href").should("include", "gitlab.com");
            });
    });

    it("should navigate to /repo after login", () => {
        cy.intercept(
            {
                method: "GET",
                url: "**/git/repos",
            },
            (req) => {
              req.reply({
                  statusCode: 200,
                  body: ["repo1", "repo2", "repo3"],
              });
          }
        ).as("getRepos");
        cy.intercept(
            {
                method: "GET",
                url: "**/identity/",
            },
            (req) => {
                req.reply({
                    statusCode: 200,
                    body: {
                        uid: "testUid",
                        login: "testUser",
                        email: "test@example.com",
                        provider: "testProvider",
                    },
                });
            },
        );

        cy.intercept("GET", "**/login/github", (req) => {
            req.reply({
                statusCode: 302,
                headers: {
                    location:
                        "http://localhost:3000/login_callback?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJPbmxpbmUgSldUIEJ1aWxkZXIiLCJpYXQiOjE3MDU0NDQ5NTUsImV4cCI6MTczNjk4MDk1MSwiYXVkIjoiIiwic3ViIjoiIn0.Uarxpkzo4Vei2WL9niQ8PPpH72f3juNXnV1TVsKHL28&exp=1736980951&iat=1705444955", // Ustaw parametry jakie potrzebujesz
                },
            });
        });

        cy.visit("http://localhost:3000/");
        cy.get('button:contains("Login with GitHub")').click();

        cy.url().should("include", "/login_callback");
        
        cy.url().should("include", "/repo");
        cy.wait("@getRepos");
        cy.contains("Choose your Repository");
    });
});
