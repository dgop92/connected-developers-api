const apiUrl = `${Cypress.env("apiUrl")}`

describe('Register endpoint', () => {

    const realDev1 = 'MGetwith'
    const realDev2 = 'MGetwith1'
    const basePath = '/connected/register'

    const buildBasePath = (dev1, dev2) => {
        return `${apiUrl}${basePath}/${dev1}/${dev2}`
    }

    it('should return the request of the two connected devs', () => {
        cy.request({
            failOnStatusCode: false,
            method: 'GET',
            url: `${apiUrl}/connected/realtime/${realDev1}/${realDev2}`
        }).then((response) => {
            expect(response.status).to.eq(200)
        })

        cy.request({
            failOnStatusCode: false,
            method: 'GET',
            url: buildBasePath(realDev1, realDev2)
        }).then((response) => {
            expect(response.status).to.eq(200)
            expect(response.body).to.have.length.of.at.least(1)
            expect(response.body.map(a => a.organisations).flat()).to.include.members(['thisisatestorgname'])
        })
    })

    it('should return empty array if not registered', () => {
        cy.request({
            failOnStatusCode: false,
            method: 'GET',
            url: buildBasePath('random1', 'random2')
        }).then((response) => {
            expect(response.status).to.eq(404)
            expect(response.body).to.be.empty
        })
    })
})
