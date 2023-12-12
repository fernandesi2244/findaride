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

export function getDateDiff(startString, endString) {
    const start = new Date(startString)
    const end = new Date(endString)
    const diff = Math.round((end - start) / (1000 * 60 * 60 * 24))
    if(diff > 0) {
        return "+" + String(diff)
    }
    return ""
}

const months = {
    1: "Jan",
    2: "Feb",
    3: "Mar",
    4: "Apr",
    5: "May",
    6: "Jun",
    7: "Jul",
    8: "Aug",
    9: "Sep",
    10: "Oct",
    11: "Nov",
    12: "Dec"
}

export function getDateRange(startString, endString) {
    return getDate(startString) + "  " + getTime(startString) + " – " + getTime(endString)
}

export function getTimeRange(startString, endString) {
    return getTime(startString) + " – " + getTime(endString)
}

export function getDate(dateString) {
    const date = new Date(dateString)
    return months[date.getMonth()] + ". " + date.getDate() + " " + date.getFullYear() 
    // return new Date(dateString).toLocaleDateString();
}

export function getDateOrRange(firstDateString, secondDateString) {
  // if the two dates are the same, just return the date
  if (getDate(firstDateString) === getDate(secondDateString)) {
    return getDate(firstDateString);
  }

  // otherwise, return the date range
  return `${getDate(firstDateString)} - ${getDate(secondDateString)}`;
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
  return new Date(dateString).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
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