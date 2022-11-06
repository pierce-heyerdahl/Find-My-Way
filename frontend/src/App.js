import React, { useState, useEffect } from 'react'

function App() {

	const [data, setData] = useState([{}])

	useEffect(() => {
		fetch("/test").then(
			res => res.json()
		).then(
			data => {
				setData(data)
				console.log(data)
			}
		)
	}, [])

	return (
		<div>
			{(typeof data.numbers === 'undefined') ? (
				<p>Loading...</p>
			) : (
				data.numbers.map((number, i) => (
					<p key={i}>{number}</p>
				))
			)}
		</div>
	)
}

export default App
