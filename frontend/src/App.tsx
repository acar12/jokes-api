import { useEffect, useState } from "react"
import Card from "react-bootstrap/Card"

interface Joke {
    id: number,
    name: string,
    joke: string,
    created_at: string
}

function App() {
    const [jokes, setJokes] = useState<Joke[]>([])

    useEffect(() => {
        fetch("/api/jokes/").then(res => res.json()).then(json => {
            setJokes(json)
        })
    }, [])

    return (<div className="container mt-4">
        <h1>Jokes</h1>
        <div className="container">
            {jokes.length > 0 && jokes.map(joke => 
                <Card key={joke.id}>
                    <Card.Body>
                        <Card.Title>{joke.name}</Card.Title>
                        <Card.Text>{joke.joke}</Card.Text>
                    </Card.Body>
                    <Card.Footer>{joke.created_at}</Card.Footer>
                </Card>
            )}
        </div>
    </div>)
}

export default App
