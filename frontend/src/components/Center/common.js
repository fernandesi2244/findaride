export function getDate(dateString) {
    return new Date(dateString).toLocaleDateString();
  }
  
export function getTime(dateString) {
    return new Date(dateString).toLocaleTimeString();
}
  
export function getDateTime(dateString) {
    return new Date(dateString).toLocaleString();
}
  
export function cleanLocation(location) {
    let tokens = location.split(",");
    tokens.splice(-1);
  
    return tokens.join(",");
}