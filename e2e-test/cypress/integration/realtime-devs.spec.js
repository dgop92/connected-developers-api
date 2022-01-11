const apiUrl = `${Cypress.env("apiUrl")}`

describe('Realtime endpoint', () => {

    const realDev1 = 'MGetwith'
    const realDev2 = 'MGetwith1'
    const fakeDev2 = 'ñlaskfleoei'
    const basePath = '/connected/realtime'

    const buildBasePath = (dev1, dev2) => {
        return `${apiUrl}${basePath}/${dev1}/${dev2}`
    }

    it('should return the org when two devs are connected', () => {
        cy.request({
            failOnStatusCode: false,
            method: 'GET',
            url: buildBasePath(realDev1, realDev2)
        }).then((response) => {
            expect(response.status).to.eq(200)
            expect(response.body).to.have.property('connected').to.true
            expect(response.body.organisations).to.contain('thisisatestorgname')
        })
    })

    it('should return 400 if one handle does not exist', () => {
        cy.request({
            failOnStatusCode: false,
            method: 'GET',
            url: buildBasePath(realDev1, fakeDev2)
        }).then((response) => {
            expect(response.status).to.eq(400)
            expect(response.body).to.have.property('errors')
            expect(response.body.errors).contain(
                `${fakeDev2} is not a valid user in github`
            )
            expect(response.body.errors).contain(
                `${fakeDev2} is not a valid user in twitter`
            )
        })
    })

    it('should return 400 if one handle does not exist in github', () => {
        cy.request({
            failOnStatusCode: false,
            method: 'GET',
            url: buildBasePath('chosco_', 'castarco')
        }).then((response) => {
            expect(response.status).to.eq(400)
            expect(response.body.errors).contain(
                'chosco_ is not a valid user in github'
            )
        })
    })

    it('should return 404 if they are not connected', () => {
        cy.request({
            failOnStatusCode: false,
            method: 'GET',
            url: buildBasePath('flavio', 'castarco')
        }).then((response) => {
            expect(response.status).to.eq(404)
            expect(response.body).to.have.property('connected').to.false
        })
    })
})
