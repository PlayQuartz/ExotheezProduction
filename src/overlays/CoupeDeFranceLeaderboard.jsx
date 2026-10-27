import { useState } from 'react'
import './coupe-de-france.css'

const placeholderTeams = Array.from({ length: 10 }, (_, index) => ({
  id: `placeholder-${index}`, name: 'Player Name', eliminations: 0, points: 0,
}))

export function CoupeDeFranceLeaderboard({ data, onPageChange }) {
  const [requestedPage, setPage] = useState(0)
  const sorted = [...data.standings].sort((a, b) => b.points - a.points)
  const lastPage = Math.max(0, Math.ceil(sorted.length / 10) - 1)
  const page = data.pagination?.page ?? Math.min(requestedPage, lastPage)
  const rows = data.pagination ? data.standings : sorted.slice(page * 10, (page + 1) * 10)
  const teams = rows.length || data.pagination ? rows : placeholderTeams
  const previousDisabled = data.pagination ? !data.pagination.hasPrevious : page === 0
  const nextDisabled = data.pagination ? !data.pagination.hasNext : page === lastPage
  const changePage = data.pagination ? onPageChange : setPage
  return <section className="cdf-leaderboard" aria-label="Coupe de France Fortnite 2026 — classement">
    <img className="cdf-artwork" src="/events/coupe-de-france-fortnite-2026/leaderboard-artwork.png" alt="Coupe de France Fortnite 2026. Classement : les 10 premiers duos. Colonnes : rang, duo, éliminations, total. Classement provisoire." />
    <button className="cdf-page-control cdf-previous" aria-label="Previous leaderboard page" disabled={previousDisabled} onClick={() => changePage(page - 1)} />
    <button className="cdf-page-control cdf-next" aria-label="Next leaderboard page" disabled={nextDisabled} onClick={() => changePage(page + 1)} />
    <ol className="cdf-standings" start={page * 10 + 1}>{teams.map((team, index) => <li className="cdf-row" key={team.id}>
      <span className="cdf-rank">{String(team.rank ?? (page * 10 + index + 1)).padStart(2, '0')}</span>
      <span className="cdf-duo" title={team.name}>{team.name}</span>
      <span className="cdf-eliminations" aria-label="Éliminations">{team.eliminations ?? '–'}</span>
      <span className="cdf-total" aria-label="Total">{team.points}</span>
    </li>)}</ol>
  </section>
}
