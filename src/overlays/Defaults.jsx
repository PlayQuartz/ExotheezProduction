function Standings({ data, compact }) {
  const teams = [...data.standings].sort((a, b) => b.points - a.points)
  return <table><thead><tr><th>Rank</th><th>Team</th><th>Points</th></tr></thead><tbody>{teams.slice(0, compact ? 5 : undefined).map((team, i) => <tr key={team.id}><td>{i + 1}</td><td>{team.name}</td><td>{team.points}</td></tr>)}</tbody></table>
}

export function Leaderboard({ event, data }) {
  return <section className="panel leaderboard"><header><span>{event.name}</span><h1>Leaderboard</h1><p>Game {data.gameNumber}</p></header><Standings data={data} /></section>
}
export function PopupLeaderboard({ event, data }) {
  return <section className="panel popup"><header><span>{event.name} / Game {data.gameNumber}</span><h1>Leaderboard</h1></header><Standings data={data} compact /></section>
}
export function GameNumber({ event, data }) {
  return <section className="panel game"><span>{event.name}</span><h1>Game {data.gameNumber}</h1></section>
}
