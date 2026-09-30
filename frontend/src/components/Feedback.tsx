export function Feedback({ message, onRetry }: { message: string; onRetry?: () => void }) {
  return <div className="feedback" role={onRetry ? 'alert' : 'status'}>
    <p>{message}</p>
    {onRetry && <button className="button" onClick={onRetry}>Retry</button>}
  </div>;
}
