import {useState} from "react";

function App() {
    const [text, setText] = useState('')
    fetch(import.meta.env.VITE_APP_API_URL + '/hello').then(res => res.text()).then(setText)
    return (
    <p>
        {text}
    </p>
  )
}

export default App
