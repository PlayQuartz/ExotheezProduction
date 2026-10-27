import { Leaderboard, PopupLeaderboard, GameNumber } from './Defaults.jsx'
import { CoupeDeFranceLeaderboard } from './CoupeDeFranceLeaderboard.jsx'
import { CoupeDeFranceGameNumber } from './CoupeDeFranceGameNumber.jsx'
import { CoupeDeFrancePopup } from './CoupeDeFrancePopup.jsx'

// Add PSD layout components here, then select their key in events.js.
export const layouts = { leaderboard: { default: Leaderboard, 'coupe-de-france-top10': CoupeDeFranceLeaderboard }, 'popup-leaderboard': { compact: PopupLeaderboard, 'coupe-de-france-popup': CoupeDeFrancePopup }, 'game-number': { default: GameNumber, 'coupe-de-france-game-number': CoupeDeFranceGameNumber } }

