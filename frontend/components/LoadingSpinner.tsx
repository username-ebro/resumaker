export function LoadingSpinner({ message }: { message: string }) {
  return (
    <div className="brutal-box brutal-shadow p-8 bg-yellow-100">
      <div className="flex flex-col items-center">
        <div className="w-12 h-12 border-4 border-black border-t-transparent rounded-full animate-spin mb-4" />
        <p className="text-sm font-bold uppercase text-center">{message}</p>
      </div>
    </div>
  );
}
