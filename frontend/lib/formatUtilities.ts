import { DateTime } from "luxon";

export function formatDate(date: string) {
  const datetime = DateTime.fromISO(date);
  if (datetime.year == DateTime.now().year) {
    return datetime.toFormat("LLL d");
  }
  return datetime.toFormat("LLL d, yyyy");
}

export function formatDateDiff(date: string) {
  return DateTime.fromISO(date).toRelative(DateTime.now());
}

// export function formatDuration(duration: Duration) {
//   function pad(n: number) {
//     const s = `0${n}`;
//     return s.substring(s.length - 2);
//   }
//   const d = duration;
//   if (d.hours == 0) {
//     return `${d.minutes}:${pad(d.seconds)}`;
//   }
//   return `${d.hours}:${pad(d.minutes)}:${pad(d.seconds)}`;
// }

export function formatNumberCompact(n: number) {
  const formatter = Intl.NumberFormat("en", { notation: "compact" });
  return formatter.format(n);
}
