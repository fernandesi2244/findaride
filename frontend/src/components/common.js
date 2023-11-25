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
  
    return tokens[0];
}

export function nameList(participants) {
    let names = [];

    for (let participant of participants) {
        names.push(`${participant.first_name} ${participant.last_name}`);
    }

    return names.join(", ")
}