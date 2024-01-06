export function getLocalStorageObject<T>(key: string): T | undefined {
    const item = localStorage.getItem(key);
    if (item) {
        try {
            return JSON.parse(item);
        } catch (e) {
            throw new Error(`Error parsing token in localStorage`);
        }
    }
    return undefined;
}

export function setLocalStorageObject<T>(key: string, obj: T) {
    localStorage.setItem(key, JSON.stringify(obj));
}