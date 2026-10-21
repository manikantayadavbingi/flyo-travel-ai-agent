
const $ = (id) => document.getElementById(id);

const flightForm = $("flight-form");
const reconciliationForm = $("reconciliation-form");

function showMessage(id, message = "") {
    $(id).textContent = message;
}

function setApiStatus(message, online) {
    $("api-status-text").textContent = message;
    const dot = document.querySelector(".api-status .status-dot");
    dot.style.background = online ? "#20b779" : "#d9534f";
}

async function requestJSON(url, options = {}) {
    const response = await fetch(url, {
        ...options,
        headers: {
            "Content-Type": "application/json",
            ...(options.headers || {}),
        },
    });

    const data = await response.json().catch(() => ({}));

    if (!response.ok) {
        const detail = data.detail;
        const message = Array.isArray(detail)
            ? detail.map((item) => item.msg).join("; ")
            : detail || `Request failed (${response.status})`;
        throw new Error(message);
    }

    return data;
}

async function checkAPI() {
    try {
        await requestJSON("/");
        setApiStatus("API connected", true);
    } catch {
        setApiStatus("API unavailable", false);
    }
}

// Navigation between the two workspace sections.
document.querySelectorAll(".nav-item").forEach((button) => {
    button.addEventListener("click", () => {
        const section = button.dataset.section;

        document.querySelectorAll(".nav-item").forEach((item) => {
            item.classList.toggle("active", item === button);
        });

        $("flights-section").classList.toggle("hidden", section !== "flights");
        $("reconciliation-section").classList.toggle(
            "hidden",
            section !== "reconciliation"
        );

        $("page-title").textContent =
            section === "flights" ? "Flight search" : "Reconciliation";
    });
});

// Default date: tomorrow in the user's local timezone.
const tomorrow = new Date();
tomorrow.setDate(tomorrow.getDate() + 1);
const localDate = [
    tomorrow.getFullYear(),
    String(tomorrow.getMonth() + 1).padStart(2, "0"),
    String(tomorrow.getDate()).padStart(2, "0"),
].join("-");

$("travel-date").min = localDate;
$("travel-date").value = localDate;

function createElement(tag, className, text) {
    const element = document.createElement(tag);
    if (className) element.className = className;
    if (text !== undefined) element.textContent = text;
    return element;
}

function renderEmpty(container, title, description) {
    container.replaceChildren();

    const card = createElement("div", "empty-state");
    card.append(
        createElement("span", "empty-icon", "✈"),
        createElement("h3", "", title),
        createElement("p", "", description)
    );

    container.append(card);
}

function renderFlights(data) {
    const container = $("flight-results");
    container.replaceChildren();

    $("flight-count").textContent =
        `${data.count} ${data.count === 1 ? "flight" : "flights"}`;
    $("flight-results-title").textContent =
        data.count ? "Flights for your journey" : "No matching flights";

    if (!data.flights.length) {
        renderEmpty(
            container,
            "No flights found",
            "Try another date, route, or budget."
        );
        return;
    }

    data.flights.forEach((flight) => {
        const card = createElement("article", "flight-card");
        const info = createElement("div");
        const top = createElement("div", "flight-topline");

        top.append(
            createElement("span", "flight-number", flight.flight_number),
            createElement("span", "flight-airline", flight.airline)
        );

        const route = createElement("div", "flight-route");
        const origin = createElement("div");
        origin.append(
            createElement("div", "airport-code", flight.origin),
            createElement("div", "flight-time", flight.departure)
        );

        const line = createElement("div", "route-line", "→");
        const destination = createElement("div");
        destination.append(
            createElement("div", "airport-code", flight.destination),
            createElement("div", "flight-time", flight.date)
        );

        route.append(origin, line, destination);
        info.append(top, route);

        const price = createElement("div", "flight-price");
        price.append(
            createElement(
                "strong",
                "",
                Number(flight.price).toLocaleString("en-IN", {
                    style: "currency",
                    currency: "INR",
                    maximumFractionDigits: 0,
                })
            ),
            createElement("span", "", "Sample fare")
        );

        card.append(info, price);
        container.append(card);
    });
}

flightForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    showMessage("flight-message");

    const button = flightForm.querySelector('button[type="submit"]');
    button.disabled = true;
    button.querySelector("span").textContent = "Searching...";

    const payload = {
        origin: $("origin").value.trim().toUpperCase(),
        destination: $("destination").value.trim().toUpperCase(),
        travel_date: $("travel-date").value,
    };

    const budget = $("max-price").value;
    if (budget !== "") payload.max_price = Number(budget);

    try {
        const data = await requestJSON("/flights/search", {
            method: "POST",
            body: JSON.stringify(payload),
        });
        renderFlights(data);
    } catch (error) {
        showMessage("flight-message", error.message);
        renderEmpty(
            $("flight-results"),
            "Search could not be completed",
            "Check the API connection and your search details."
        );
        $("flight-count").textContent = "Unavailable";
    } finally {
        button.disabled = false;
        button.querySelector("span").textContent = "Search flights";
    }
});

function makeRecord(prefix) {
    return {
        booking_id: $(`${prefix}-id`).value.trim(),
        passenger: $(`${prefix}-passenger`).value.trim(),
        flight_number: $(`${prefix}-flight`).value.trim(),
        amount: Number($(`${prefix}-amount`).value),
        status: $(`${prefix}-status`).value,
    };
}

function displayValue(value) {
    if (value === "MISSING") return "Missing field";
    if (value === null || value === undefined) return "Not provided";
    return String(value);
}

function renderReconciliation(result) {
    const container = $("reconciliation-results");
    container.replaceChildren();

    const card = createElement(
        "div",
        `reconciliation-result ${result.matched ? "match" : "mismatch"}`
    );

    const status = createElement("div", "result-status");
    status.append(
        createElement("span", "result-symbol", result.matched ? "✓" : "⚠"),
    );

    const summary = createElement("div");
    summary.append(
        createElement(
            "h3",
            "",
            result.matched ? "Records match" : "Review required"
        ),
        createElement(
            "p",
            "",
            result.matched
                ? `Booking ${result.booking_id} matches across the checked fields.`
                : `Booking ${result.booking_id} has ${result.mismatches.length} detected difference(s).`
        )
    );

    status.append(summary);
    card.append(status);

    if (result.mismatches.length) {
        const list = createElement("div", "mismatch-list");

        result.mismatches.forEach((item) => {
            const row = createElement("div", "mismatch-item");
            row.append(createElement("div", "mismatch-field", item.field));

            const values = createElement("div", "mismatch-values");
            const bookingValue = createElement("div");
            bookingValue.append(
                createElement("span", "", "Your booking"),
                createElement("strong", "", displayValue(item.booking_value))
            );

            const supplierValue = createElement("div");
            supplierValue.append(
                createElement("span", "", "Supplier record"),
                createElement("strong", "", displayValue(item.supplier_value))
            );

            values.append(bookingValue, supplierValue);
            row.append(values);

            if (item.issue) {
                row.append(
                    createElement(
                        "span",
                        "issue-tag",
                        item.issue.replaceAll("_", " ")
                    )
                );
            }

            list.append(row);
        });

        card.append(list);
    }

    container.append(card);
}

reconciliationForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    showMessage("reconciliation-message");

    const button = reconciliationForm.querySelector('button[type="submit"]');
    button.disabled = true;
    button.querySelector("span").textContent = "Comparing...";

    const booking = makeRecord("booking");
    const supplierRecord = makeRecord("supplier");

    // This demo expects matching booking IDs; IDs aren't compared
    // by the current reconciliation function itself.
    if (booking.booking_id !== supplierRecord.booking_id) {
        showMessage(
            "reconciliation-message",
            "Booking IDs differ. Verify that both records refer to the same booking."
        );
        button.disabled = false;
        button.querySelector("span").textContent = "Compare records";
        return;
    }

    try {
        const result = await requestJSON("/reconciliation/check", {
            method: "POST",
            body: JSON.stringify({
                booking,
                supplier_record: supplierRecord,
            }),
        });

        renderReconciliation(result);
    } catch (error) {
        showMessage("reconciliation-message", error.message);
    } finally {
        button.disabled = false;
        button.querySelector("span").textContent = "Compare records";
    }
});

checkAPI();
