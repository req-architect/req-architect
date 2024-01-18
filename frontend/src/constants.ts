const env = import.meta.env;

function constant(name: string) {
    return env[name];
}

export { constant };
