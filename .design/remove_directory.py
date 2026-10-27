from pathlib import Path
p=Path('src/App.jsx')
s=p.read_text(encoding='utf-8')
start=s.index('const types =')
s=s[:start]+'''export default function App() {
  const path = location.pathname.replace(/\\/+$/, '') || '/'
  if (path === '/') return null

  const match = path.match(/^\\/overlays\\/([^/]+)\\/([^/]+)$/)
  const event = match && events[match[1]]
  const type = match?.[2]
  if (event && Object.hasOwn(layouts, type) && Object.hasOwn(layouts[type], event.layouts[type])) {
    return <Overlay event={event} type={type} />
  }
  return null
}
'''
p.write_text(s,encoding='utf-8')
p=Path('src/App.css'); s=p.read_text(encoding='utf-8'); s=s[s.index('.viewport {'):]; p.write_text(s,encoding='utf-8')
p=Path('README.md'); s=p.read_text(encoding='utf-8').replace('Open the URL Vite prints for the overlay library.', 'The root URL is intentionally blank. Open a direct overlay URL to display an overlay.'); p.write_text(s,encoding='utf-8')
