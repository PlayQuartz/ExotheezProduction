import './coupe-de-france.css'

export function CoupeDeFranceGameNumber({ data }) {
  const value = new URLSearchParams(location.search).get('totalGames')
  const parsed = Number(value)
  const totalGames = /^\d+$/.test(value ?? '') && Number.isSafeInteger(parsed) && parsed > 0 ? parsed : 10
  const currentGameText = String(data.gameNumber).padStart(2, '0')
  const totalGamesText = String(totalGames).padStart(2, '0')

  return <section className="cdf-game-number" aria-label={`Manche ${data.gameNumber} sur ${totalGames}`}>
    <div className="cdf-game-content">
    <img src="/events/coupe-de-france-fortnite-2026/game-number-artwork.png" width="303" height="77" alt="" />
    <span className="cdf-game-current" style={{ fontSize: `${41.56 * Math.min(1, 2 / currentGameText.length)}px` }}>{currentGameText}</span>
    <span className="cdf-game-total" style={{ fontSize: `${30.68 * Math.min(1, 2 / totalGamesText.length)}px` }}>{totalGamesText}</span>
    </div>
  </section>
}
