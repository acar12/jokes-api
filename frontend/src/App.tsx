import { useEffect, useState } from "react"
import { useForm, FieldValues } from "react-hook-form"
import Form from "react-bootstrap/Form"
import Card from "react-bootstrap/Card"
import Button from "react-bootstrap/Button"
import apiURL from "./util"

interface Joke {
    id: number,
    name: string,
    joke: string,
    created_at: string
}

const JokeForm = ({ refreshJokes }: { refreshJokes: () => Promise<void> }) => {
    const { register, handleSubmit } = useForm()
    const insertJoke = (data: FieldValues) => fetch(apiURL("api/jokes/"), {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ name: data.name, joke: data.joke})
    }).then(refreshJokes)

    return (
        <Form onSubmit={handleSubmit(insertJoke)} className="mb-3">
            <div className="row">
                <div className="col">
                    <Form.Control {...register("name")} />
                </div>
                <div className="col">
                    <Form.Control {...register("joke")} />
                </div>
                <div className="col">
                    <Button type="submit">Submit</Button>
                </div>
            </div>
        </Form>
    )
}

const JokeCard = ({ joke, refreshJokes }: { joke: Joke, refreshJokes: () => Promise<void> }) => {
    const formatDatetimeOptions: Intl.DateTimeFormatOptions = {
        weekday: "long", year: "numeric", month: "long", day: "numeric",
        hour: "numeric", minute: "numeric", hour12: true
    }
    const deleteJoke = (id: number) => fetch(apiURL(`api/jokes/${id}`), { method: "DELETE" }).then(refreshJokes)

    return (
        <Card key={joke.id} className="mt-2 mb-3">
            <Card.Body>
                <Card.Title>{joke.name}</Card.Title>
                <Card.Text>{joke.joke}</Card.Text>
                <Card.Link onClick={() => deleteJoke(joke.id)}>Delete</Card.Link>
            </Card.Body>
            <Card.Footer>{(new Date(joke.created_at)).toLocaleString(undefined, formatDatetimeOptions)}</Card.Footer>
        </Card>
    )
}

function App() {
    const [jokes, setJokes] = useState<Joke[]>([])
    const refreshJokes = () => fetch(apiURL("/api/jokes/")).then(res => res.json()).then(setJokes)


    useEffect(() => {refreshJokes()}, [])

    return (
        <div className="container">
            <h1 className="my-4">Jokes</h1>
            <JokeForm refreshJokes={refreshJokes} />
            <div className="container">
                {jokes.map(joke => <JokeCard key={joke.id} joke={joke} refreshJokes={refreshJokes} />)}
            </div>
        </div>
    )
}

export default App
