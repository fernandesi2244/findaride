export function formatError(errorDict) {
    if (typeof errorDict === "string") {
      return errorDict;
    }
    try {
      let errorString = "";
      let errorNum = 1;
      for (const [key, value] of Object.entries(errorDict)) {
        errorString += `${errorNum++} ${value}\n`;
      }
      return errorString;
    } catch (error) {
      return JSON.stringify(errorDict);
    }
  }

export function getDate(dateString) {
    return new Date(dateString).toLocaleDateString();
}

export function getDatePart(firstDateString, secondDateString) {
    // if the two dates are the same, just return the date
    if (getDate(firstDateString) === getDate(secondDateString)) {
        return "on " + getDate(firstDateString);
    }

    // otherwise, return the date range
    return `(${getDate(firstDateString)}-${getDate(secondDateString)})`;

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

export function nameEmail(participant) {
    return `${participant.first_name} ${participant.last_name} (${participant.email})`;
}

export function nameList(participants) {
    let names = [];

    for (let participant of participants) {
        names.push(`${participant.first_name} ${participant.last_name}`);
    }

    return names.join(", ")
}