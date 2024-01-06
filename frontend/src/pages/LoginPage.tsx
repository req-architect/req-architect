export default function LoginPage() {
    return (
        <>
            <a
                href={
                    import.meta.env.VITE_APP_API_URL + "/MyServer/login/github"
                }
            >
                Login with GitHub
            </a>
            <br />
            <a
                href={
                    import.meta.env.VITE_APP_API_URL + "/MyServer/login/gitlab"
                }
            >
                Login with GitLab
            </a>
        </>
    );
}
